modules/patent/api/views_legal.py imports plain functions (record_office_action, prepare_response, approve_response, submit_response, record_grant, schedule_maintenance, decide_renewal) from modules/patent/services/post_filing.py, but that file defines them as static methods of the class PostFilingService. Keep the class exactly as it is and add these lines at the very end of modules/patent/services/post_filing.py, after the class:

record_office_action = PostFilingService.record_office_action
prepare_response = PostFilingService.prepare_response
approve_response = PostFilingService.approve_response
submit_response = PostFilingService.submit_response
record_grant = PostFilingService.record_grant
schedule_maintenance = PostFilingService.schedule_maintenance
decide_renewal = PostFilingService.decide_renewal
get_history = PostFilingService.get_history
