FIT is our capstone project: a calorie tracking website utilizing a couple different API's to calculate the calorie intake and output of the user, and providing a customized graph the user can view.

#Pips that were used
pip install sqlalchemy
pip install Flask
pip install flask-login
pip install WTForms
pip install DateTime
pip install pandas
pip install Flask-Mail
pip install itsdangerous
pip install matplotlib
pip install email-validator
pip install requests

Its backend utilizes Python, along with MySQL to allow a user to be created with a valid email, since there is email authentification. Once logged in, you will be greeted by a homepage that has your current calorie graph (if you are a returning user).

![giphy](https://github.com/FMass-3355/CSC400/assets/98336203/df2d80ac-f6fd-44cd-b5c2-02f685ae3cdf)

Continuing through the site, you will find the Tracker page, where you edit/view your daily calorie habits. You may add/remove foods or exercises done for that day and it will automatically calculate the calories consumed/burned using a health API. This calculation is then sent to the graph that is updated automatically as soon as you finish.

![gif2](https://github.com/FMass-3355/CSC400/assets/98336203/017f489d-2150-4e14-9fcb-5e83f7fc2214)

For the profile, you are able to view/edit your basic details, like your name, height, and weight. You can also search for other users and view your friends' profile. Viewing their profile provides you with their graph so you can keep up to date with their calorie habits and see how you compare.

![giphy3](https://github.com/FMass-3355/CSC400/assets/98336203/ea7b10ad-78de-4b98-a537-383defa22963)

Lastly there is an admin role, that is able to add and delete users from the site if need be. Deleting a user will naturally remove all information regarding them from the database.

![giphy4](https://github.com/FMass-3355/CSC400/assets/98336203/5d1571f8-a713-490d-943a-5272a24e3ccc)

If you wish to run it locally, you will have to set up a "fit" database schema and make sure you have all the required pip modules installed (list located above). 
