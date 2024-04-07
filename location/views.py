from django.shortcuts import render, HttpResponse
from django.contrib.gis.geoip2 import GeoIP2
from django.http import JsonResponse

def home(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    device_type = ""
    browser_type = ""
    browser_version = ""
    os_type = ""
    os_version = ""
    if request.user_agent.is_mobile:
        device_type = "Mobile"
    if request.user_agent.is_tablet:
        device_type = "Tablet"
    if request.user_agent.is_pc:
        device_type = "PC"
    
    browser_type = request.user_agent.browser.family
    browser_version = request.user_agent.browser.version_string
    os_type = request.user_agent.os.family
    os_version = request.user_agent.os.version_string
    
    g = GeoIP2()
    location = g.city(ip)
    location_country = location["country_name"]
    location_city = location["city"]
    latitude = location["latitude"]
    longitude = location["longitude"]
    
    context = {
        "ip": ip,
        "device_type": device_type,
        "browser_type": browser_type,
        "browser_version": browser_version,
        "os_type":os_type,
        "os_version":os_version,
        "location_country": location_country,
        "location_city": location_city,
        "latitude": latitude,
        "longitude": longitude
    }
    return render(request, "home.html", context)

def update_location(request):
  if request.method == 'POST':
      data = request.POST
      latitude = data.get('latitude')
      longitude = data.get('longitude')

  
      response_data = {
          'status': 'success',
          'latitude': latitude,
          'longitude': longitude
      }
      return JsonResponse(response_data)
  else:
      response_data = {'status': 'error', 'message': 'Method not allowed'}
      return JsonResponse(response_data, status=405)
