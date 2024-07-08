from django.shortcuts import render
from django.http import HttpResponse
import subprocess
from django.views.decorators.csrf import csrf_exempt
# Create your views here


from django.shortcuts import render, redirect
from .form import UserDetailsForm
def home(request):
    return HttpResponse('Hello, from home!')

def user_details_view(request):
    if request.method == 'POST':
        form = UserDetailsForm(request.POST)
        if form.is_valid():
            # Process the form data
            pass
    else:
        form = UserDetailsForm()

    return render(request, 'userForm.html', {'form': form})

def success_view(request):
    return render(request, 'success.html')



def config_nginx(request):
    if(request.method == 'POST'):
        form =UserDetailsForm(request.POST)
        if form.is_valid():
            operating_system = form.cleaned_data['operating_system']
            request_limit = form.cleaned_data['request_limit']
            request_limit_unit = form.cleaned_data['request_limit_unit']
            proxy_URL = form.cleaned_data['proxy_URL']
            end_point = form.cleaned_data['end_point']
            block_all_private_ips = form.cleaned_data['block_all_private_ips']
            number_of_private_ips = form.cleaned_data['number_of_private_ips']
            block_all_public_ips = form.cleaned_data['block_all_public_ips']
            number_of_public_ips = form.cleaned_data['number_of_public_ips']
            print("hi from config_nginx ")

            private_ips = []
            public_ips = []

            for key, value in request.POST.items():
                if key.startswith('private_ip_'):
                    private_ips.append(value)
                elif key.startswith('public_ip_'):
                    public_ips.append(value)

            if operating_system == 'linux':
                nginx_config = generate_nginx_config(
                    request_limit,
                    request_limit_unit,
                    proxy_URL,
                    end_point,
                    block_all_private_ips,
                    private_ips,
                    block_all_public_ips,
                    public_ips
                )
                reload_nginx()

                if write_nginx_config(nginx_config):
                    reload_nginx()
                    return HttpResponse("NGINX configuration updated successfully!")
                else:
                    return HttpResponse("Failed to write NGINX configuration.", status=500)
            else:
                nginx_config = generate_nginx_config_windows(
                    request_limit,
                    request_limit_unit,
                    proxy_URL,
                    end_point,
                    block_all_private_ips,
                    private_ips,
                    block_all_public_ips,
                    public_ips
                )
                reload_nginx_windows()

                if write_nginx_config_windows(nginx_config):
                    reload_nginx_windows()
                    return HttpResponse("NGINX configuration updated successfully!")
                else:
                    return HttpResponse("Failed to write NGINX configuration.", status=500)
    else:
        form = UserDetailsForm()
    return render(request, 'userForm.html', {'form': form})

def write_nginx_config(config):
    try:
        with open('/etc/nginx/nginx.conf', 'w') as config_file:
            config_file.write(config)
        return True
    except IOError as e:
        print(f"Failed to write NGINX config: {e}")
        return False
    

def write_nginx_config_windows(config):
    try:
        with open('C:/nginx/conf/nginx.conf', 'w') as config_file:
            config_file.write(config)
        return True
    except IOError as e:
        print(f"Failed to write NGINX config: {e}")
        return False


def generate_ip_block_rules(block_all_private_ips, private_ips, block_all_public_ips, public_ips):
    rules = ""
    if block_all_private_ips == 'yes':
        rules += "deny 10.0.0.0/8;\n"
        rules += "deny 172.16.0.0/12;\n"
        rules += "deny 192.168.0.0/16;\n"
    else:
        for ip in private_ips:
            rules += f"allow {ip};\n"

  
    for ip in public_ips:
        rules += f"allow {ip};\n"
    rules += "deny all;\n"

    return rules

def generate_nginx_config(request_limit, request_limit_unit,proxy_URL,end_point,block_all_private_ips, private_ips, block_all_public_ips, public_ips):
    nginx_config_template=f"""

woker_processes auto;
pid /run/nginx.pid;

include /etc/nginx/modules-enabled/*.conf;

events{{
    worker_connections 768;

}}

http{{
    sendfile on;
    tcp_nopush on;
    types_hash_max_size 2048;
    include /etc/nginx/mime.types;

    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    gzip on;

    limit_req_zone $remote_addr zone=limitreqsbyaddr:20m rate={request_limit}{request_limit_unit};
    limit_req_status 429;

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;

    server{{
        listen 80 ;
        server_name localhost;

        location /{{
            limit_req zone=limitreqsbyaddr burst=20 nodelay;
            proxy_pass {proxy_URL};
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_connect_timeout 180;
            proxy_send_timeout 180;
            proxy_read_timeout 180;
            send_timeout 180;
        }}
        location /{end_point} {{
            proxy_pass {proxy_URL};
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
           {generate_ip_block_rules(block_all_private_ips, private_ips, block_all_public_ips, public_ips)}
        }}
        error_page 500 502 503 504 /50x.html;
        error_page 404 403 /index.html;

        location = /50x.html {{
            internal;

        }}
        location = /index.html {{
            root /var/www/html;
        }}

    }}
}}
"""
    return nginx_config_template




def reload_nginx():
    subprocess.run(['sudo','nginx','-t'])
    subprocess.run(['sudo','nginx','-s','reload'])
    return True

def generate_nginx_config_windows(request_limit, request_limit_unit,proxy_URL,end_point,block_all_private_ips, private_ips, block_all_public_ips, public_ips):
    nginx_config_template=f"""

worker_processes  1;



events {{
    worker_connections  1024;
}}


http {{
    include       mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                     '"$http_user_agent" "$http_x_real_ip"';

    access_log C:/nginx/logs/access.log main;

    sendfile        on;
    keepalive_timeout  65;



    limit_req_zone $remote_addr zone=limitreqsbyaddr:20m rate={request_limit}{request_limit_unit};
    limit_req_status 429;

    real_ip_header X-Real-IP;
    set_real_ip_from 0.0.0.0/0;
    

    server {{
        listen       80;
        server_name  localhost;
 
        location / {{
		
            limit_req zone=limitreqsbyaddr burst=5 nodelay;
            proxy_pass {proxy_URL};
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            proxy_connect_timeout 180;
            proxy_send_timeout 180;
            proxy_read_timeout 180;
            send_timeout 180;
        
        }}
	    location /IDP/connect/token{{
		    deny all;
        }}

	    location /{end_point} {{
	 
            proxy_pass {proxy_URL};
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme; 
	        {generate_ip_block_rules(block_all_private_ips, private_ips, block_all_public_ips, public_ips)}
            
        }}

	

        error_page  404 500 502 503 504 429 403 /50x.html;

	   
        location = /50x.html {{
            root C:/nginx/html;
        }}


 
    }}
}}


"""
    return nginx_config_template


def reload_nginx_windows():
    subprocess.run(['nginx','-t'])
    subprocess.run(['nginx','-s','reload'])
    return True
