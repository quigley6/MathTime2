# MathTime2

A simple python Flask-based web app for early elementary math practice.

![Main Screen](https://raw.githubusercontent.com/quigley6/MathTime2/master/doc/main_screen.png?token=ACQXGN7YOAGCMXMVAO34KH27CMWVW)

## Installation

It is highly recommended to deploy this in a virtual environment. 

Clone this repo, then install prerequisites with:

```
> pip3 -r requirements.txt
```

## Launch

Start MathTime2 as you would any flask app:
```
> flask run
```

By default, it will be available via web browser on your machine at http://127.0.0.1:5000

To expose it to your local network (i.e. the kids' computers):
```
flask run --host=0.0.0.0
```
Then it's available at <your network ip>:5000

## First Run

You'll need to register your little ones. Click the registration link on the login page. It just needs a name, no password. It's not that fancy. 

Once your child is logged in, be sure to check the Settings in the upper left, and tailor the practice problems to your child's needs. Each child has their own settings.

![Settings](https://raw.githubusercontent.com/quigley6/MathTime2/master/doc/settings.png?token=ACQXGN56HQFEY3MGUAIL2VK7CMXXW)
