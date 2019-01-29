from flask import render_template

info_template = {'title': 'Main Page'}

def render(site_name, args):
    return render_template(site_name)
