from pyramid.view import view_config


@view_config(route_name='new', renderer='new.html')
def new(request):
    #kosong = True
    from datetime import datetime

    if request.POST:
        # Check password
        if request.POST['password'] == 'go ion!':
            # Check kekosongan :D
            if request.POST['question'] and request.POST['a'] and request.POST['b'] and request.POST['c'] and request.POST['d'] and request.POST['key']:
                # Jika semua terisi, baru di save
                print request.POST['date_publish']
                if not request.POST['date_publish']:

                    date_publish = datetime.utcnow()
                    publish = "1"
                else:
                    date_publish = datetime.strptime(request.POST['date_publish'],
                            "%d-%m-%Y")
                    publish = "-1"

                new_quiz = {
                    "q": request.POST['question'],
                    "a": request.POST['a'],
                    "b": request.POST['b'],
                    "c": request.POST['c'],
                    "d": request.POST['d'],
                    "key": request.POST['key'],
                    "date_publish": date_publish,
                    "publish": publish

                }
                request.db['quiz_doc'].save(new_quiz)

    return {}


@view_config(route_name='quiz', renderer='index.html')
def get_home(request):
    answer = request.db['quiz_doc'].find({"publish": "1"}).sort("_id", -1)[0]
    #print answer
    return {'q': answer['q'],
            'a': answer['a'],
            'b': answer['b'],
            'c': answer['c'],
            'd': answer['d'],
            'username': request.matchdict['username'],
            'q_id': answer['_id'],
            "account_type": request.matchdict['account_type']
            }


@view_config(route_name='posting', renderer='posting.html')
def posting(request):
    key = ''
    point = 0
    if request.POST:
        import bson
        from datetime import datetime

        # Find username
        users = request.db['user_doc'].find({"username": request.POST['username']})
        # if exist
        if users.count() > 0:
            # if quiz not taken with given username
            quiz_taken = request.db['user_doc'].find({"quiz_taken.quiz_id": bson.ObjectId(request.POST['q_id'])})

            if quiz_taken.count() < 1:
                # check if the answer = key
                quiz = request.db['quiz_doc'].find_one({"_id": bson.ObjectId(request.POST['q_id'])})

                point = 0
                key = quiz['key']
                if request.POST['answer'] == quiz['key']:
                    point = 5
                else:
                    point = 1

                # update quiz_taken
                user_doc = request.db['user_doc'].find_one({"username": request.POST['username']})
                total_point = user_doc['total_point'] + point
                request.db['user_doc'].update({"username": request.POST['username']},
                {
                    "$push": {
                        "quiz_taken": {
                            "quiz_id": bson.ObjectId(request.POST['q_id']),
                            "answer": request.POST['answer'],
                            "date": datetime.utcnow(),
                            "point": point
                        }
                    }, "total_point": total_point
                }, save=True)

            else:
                #cuekin
                quiz = request.db['quiz_doc'].find_one({"_id": bson.ObjectId(request.POST['q_id'])})
                key = quiz['key']

        # else insert new user and quiz_taken
        else:
            # check if the answer = key
            quiz = request.db['quiz_doc'].find_one({"_id": bson.ObjectId(request.POST['q_id'])})
            point = 0
            key = quiz['key']
            if request.POST['answer'] == quiz['key']:
                point = 5
            else:
                point = 1

            # insert
            user = {
                "username": request.POST['username'],
                "account_type": request.POST['account_type'],
                "quiz_taken": [{
                    "quiz_id": bson.ObjectId(request.POST['q_id']),
                    "answer": request.POST['answer'],
                    "date": datetime.utcnow(),
                    "point": point
                }],
                "total_point": point

            }
            request.db['user_doc'].save(user)
            #print "inserting..."

        return {'username': request.POST['username'],
            'answer': request.POST['answer'],
            'key': key,
            'point': point
        }


@view_config(route_name='notloggedin', renderer='notloggedin.html')
def notloggedin(request):

    answer = request.db['quiz_doc'].find({"publish": "1"}).sort("_id", -1)[0]
    #print answer
    return {'q': answer['q'],
            'a': answer['a'],
            'b': answer['b'],
            'c': answer['c'],
            'd': answer['d'],
            'q_id': answer['_id'],
            }


@view_config(route_name='loginerror', renderer='loginerror.html')
def loginerror(request):

    return {}


@view_config(route_name='saranghae100', renderer='saranghae100.html')
def saranghae100_view(request):

    return {}
