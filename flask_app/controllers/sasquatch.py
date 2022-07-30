from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.sasquatch import Sasquatch
from flask_app.models.users import User


@app.route('/new/sighting')
def new_sasquatch():
    if 'users_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['users_id']
    }

    return render_template('new.html',user=User.get_by_id(data))

@app.route('/create/sighting',methods=['POST'])
def create_sasquatch():
    if 'users_id' not in session:
        return redirect('/logout')
    if not Sasquatch.validate_recipe(request.form):
        return redirect('/new/sasquatch')
    data = {
        "location": request.form["location"],
        "happend": request.form["happend"],
        "count": request.form["count"],
        "date": request.form["date"],
        "users_id": session["users_id"]
    }
    sasquatch = Sasquatch.save(data)
    session['id'] = sasquatch
    # print(session)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit_sasquatch(id):
    if 'users_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['users_id']
    }
    return render_template("edit.html",edit=Sasquatch.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/sasquatch',methods=['POST'])
def update_sasquatch():
    if 'users_id' not in session:
        return redirect('/logout')
    if not Sasquatch.validate_recipe(request.form):
        return redirect('/new/sasquatch')
    data = {
        "location": request.form["location"],
        "happend": request.form["happend"],
        "count": request.form["count"],
        "date": request.form["date"],
        "users_id": session["users_id"],
        "id": session["id"]
    }
    Sasquatch.update(data)
    return redirect('/dashboard')

@app.route('/show/<int:id>')
def show_sasquatch(id):
    if 'users_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['users_id']
    }
    # print(Sasquatch.get_one_with_creator(data))
    print(data, user_data)
    return render_template("show.html",sasquatch=Sasquatch.get_one_with_creator(data),user=User.get_by_id(user_data))

@app.route('/destroy/<int:id>')
def destroy_tv(id):
    if 'users_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Sasquatch.destroy(data)
    return redirect('/dashboard')
