from flask import Flask,request, render_template
import handlertf

#get flask object
app=Flask(__name__,template_folder="templates")
store=None
global hdlr
#page for first load
@app.route('/')
def home():
    global hdlr
    hdlr=handlertf.handler()
    return render_template("index.html")



def manuplate(data):

    data=data.split("=")[1]
    global hdlr
    
    return(hdlr.convert(data))
  



@app.route("/my_function", methods=["POST"])
def my_function():
    if request.method == "POST":
        request.environ['CONTENT_TYPE'] = 'application/something_Flask_ignores'

        data=str(request.get_data())
        result=manuplate(data)
        
        return (result)
    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run()  
   