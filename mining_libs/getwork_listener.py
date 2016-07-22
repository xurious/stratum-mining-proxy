import json
import re
import time

from twisted.internet import defer
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET

from utils import username_format

import stratum.logger
log = stratum.logger.get_logger('proxy')

class Root(Resource):
    isLeaf = True
    
    def __init__(self, job_registry, workers, stratum_host, stratum_port,
                 custom_user=None, custom_password=''):
        Resource.__init__(self)
        self.job_registry = job_registry
        self.workers = workers
        self.stratum_host = stratum_host
        self.stratum_port = stratum_port
        self.custom_user = custom_user
        self.custom_password = custom_password
        
    def write_response(self, request, resp):
        request.write(resp);
        #print "RESPONSE", resp
        request.finish()

    def write_success(self, request):
        request.setResponseCode(204)
        request.finish()
    
    def write_error(self, request, message):
        resp = json.dumps({'message': message})
        request.setResponseCode(400)
        request.setHeader('content-type', 'application/json')
        request.write(resp);
        #print "ERROR", resp
        request.finish()
    
    def _on_submit(self, result, request, blockheader, worker_name, start_time):
        response_time = (time.time() - start_time) * 1000
        if result == True:
            log.warning("[%dms] Share from '%s' accepted, diff %.3g" % (response_time, username_format(worker_name), self.job_registry.difficulty))
        else:
            log.warning("[%dms] Share from '%s' REJECTED" % (response_time, username_format(worker_name)))
         
        try:   
            if result:
                self.write_success(request)
            else:
                self.write_error(request, 'rejected')
        except RuntimeError:
            # RuntimeError is thrown by Request class when
            # client is disconnected already
            pass
        
    def _on_submit_failure(self, failure, request, blockheader, worker_name, start_time):
        response_time = (time.time() - start_time) * 1000
        
        # Submit for some reason failed
        try:
            self.write_error(request, failure.getErrorMessage())
        except RuntimeError:
            # RuntimeError is thrown by Request class when
            # client is disconnected already
            pass

        log.warning("[%dms] Share from '%s' REJECTED: %s" % \
                 (response_time, username_format(worker_name), failure.getErrorMessage()))
        
    def _on_authorized(self, is_authorized, request, worker_name):
        data = request.content.read()
        
        if not is_authorized:
            self.write_error(request, "Bad worker credentials")
            return

        if not self.job_registry.last_job:
            log.warning('Getworkmaker is waiting for a job...')
            self.write_error(request, "Getworkmaker is waiting for a job...")
            return

        if request.method == 'GET':

            # getwork request
            log.info("Worker '%s' asks for new work" % username_format(worker_name))
            self.write_response(request, self.job_registry.getwork())
            return

        else:

            # submit
            d = defer.maybeDeferred(self.job_registry.submit, data, worker_name)

            start_time = time.time()
            d.addCallback(self._on_submit, request, data, worker_name, start_time)
            d.addErrback(self._on_submit_failure, request, data, worker_name, start_time)
            return

        self.write_error(request, "Unsupported method '%s'" % data['method'])
        
    def _on_failure(self, failure, request):
        self.write_error(request, "Unexpected error during authorization")
        raise failure
        
    def _prepare_headers(self, request): 
        request.setHeader('x-mining-extensions', 'longpoll')
        
    def _on_lp_broadcast(self, _, request, worker_name):
        log.info("LP broadcast for worker '%s'" % username_format(worker_name))
        
        try:
            self.write_response(request, self.job_registry.getwork())
        except RuntimeError:
            # RuntimeError is thrown by Request class when
            # client is disconnected already
            pass
        
    def render_POST(self, request):        
        return self.render_GET(request)

    def render_GET(self, request):
        self._prepare_headers(request)

        worker_name = request.args['address'][0] if 'address' in request.args else ''
        if 'worker' in request.args:
            worker_name += '.' + request.args['worker'][0]
        if 'user' in request.args:
            worker_name = request.args['user'][0]
        password = request.args['password'][0] if 'password' in request.args else ''

        if self.custom_user:
            worker_name = self.custom_user
            password = self.custom_password
 
        if worker_name == '':
            log.warning("Authorization required")
            request.setResponseCode(401)
            return "Authorization required"
        
        self._prepare_headers(request)
        
        if request.method == 'GET' and re.search('[?&]longpoll(=|&|$)', request.uri):
            log.info("Worker '%s' subscribed for LP" % username_format(worker_name))
            self.job_registry.on_block.addCallback(self._on_lp_broadcast, request, worker_name)
            return NOT_DONE_YET
       
        d = defer.maybeDeferred(self.workers.authorize, worker_name, password)
        d.addCallback(self._on_authorized, request, worker_name)
        d.addErrback(self._on_failure, request)    
        return NOT_DONE_YET
