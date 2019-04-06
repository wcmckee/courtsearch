#app.py

from flask import Flask, request, send_from_directory, render_template
from flask_bootstrap import Bootstrap
import yagmail

with open('emailtemplate.txt', 'r') as emailt:
  emailtemp = emailt.read()

app = Flask(__name__, static_url_path='/static') #create the Flask app
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def query_example():
        if request.method == 'POST':  #this block is only entered when the form is submitted
            address = request.form.get('address')
            crisis = request.form.getlist('crisis') 
            #<input type="radio" name="results" value="10" checked> 10<br>

            yag = yagmail.SMTP('exampleemail')
            yag.send(to= 'example email', subject="opt in house", contents= emailtemp + '\n\n' + address)


            return '''

                    {}


                      '''.format(address)

        return render_template('index.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) #run app in debug mode on port 5000
