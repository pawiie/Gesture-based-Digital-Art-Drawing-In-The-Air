"""
Created on Thu Apr 20 2021 15:44:36

@author: PS Chauhan
"""


from flask import Flask, render_template
from coord import liveData as ld

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html',data = (coordinates for coordinates in ld()))




