from flask import Flask, Blueprint, current_app, render_template, make_response, request, redirect, url_for
import requests
import json

qualifications = Blueprint('qualifications', __name__, url_prefix='/')