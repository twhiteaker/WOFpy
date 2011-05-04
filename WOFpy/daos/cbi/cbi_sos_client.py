import urllib
import time

class CbiSosClient(object):
    
    def __init__(self, endpoint_url):
        self.endpoint_url = endpoint_url
  
    
    def get_capabilities(self):
        
        params = urllib.urlencode({'request':'GetCapabilities',
                                   'service':'SOS'})
        
        response = urllib.urlopen(self.endpoint_url+'?%s' % params)
        
        return response
        #TODO: might be able to do series catalog from this, look at
        # ObservationOffering elements of response xml
    
    
    def describe_sensor(self, sensor_id):
        
        #?request=DescribeSensor&service=SOS&version=1.0.0&outputformat=text/xml;subtype=%22sensorML/1.0.0%22&procedure=urn:ioos:sensor:wmo:41012::adcp0
        #or
        #?request=DescribeSensor&service=SOS&version=1.0.0&outputformat=text/xml;subtype=%22sensorML/1.0.0%22&procedure=urn:ioos:station:wmo:41012
        
        params = urllib.urlencode({'request':'DescribeSensor',
                                   'service':'SOS',
                                   'version':'1.0.0',
                                   'outputformat':'text/xml;subtype="sensorML/1.0.0"',
                                   'procedure':'urn:ioos:sensor:wmo:41012::adcp0'})
        
        
    
    
    def get_observation(self, offering, observed_property, start_datetime=None,
                        end_datetime=None):
        """
        
        start_datetime and end_datetime in YYYY-MM-DDTHH:MM:SS format
            (e.g. 2010-02-11T12:00:00)
        """
        
        #http://lighthouse.tamucc.edu/sos?request=GetObservation&service=SOS&version=1.0.0&observedProperty=water_temperature&offering=014
        
        param_dict = {'request':'GetObservation',
                      'service':'SOS',
                      'version':'1.0.0',
                      'offering':offering,
                      'observedProperty':observed_property
                      }
        
        if start_datetime and end_datetime:
            event_time_string = '%s/%s' % (
                time.strftime("%Y-%m-%dT%H:%M:%SZ",
                            time.strptime(start_datetime,"%Y-%m-%dT%H:%M:%S")),
                time.strftime("%Y-%m-%dT%H:%M:%SZ",
                            time.strptime(end_datetime,"%Y-%m-%dT%H:%M:%S")))
            
            param_dict['eventtime'] = event_time_string
            
        params = urllib.urlencode(param_dict)

        response = urllib.urlopen(self.endpoint_url+'?%s' % params)
        
        return response
    
if __name__ == '__main__':
    c = CbiSosClient('http://lighthouse.tamucc.edu/sos')
    r = c.get_observation('014','water_temperature','2011-05-04T17:24:00','2011-05-04T17:36:00')
    print r.read()