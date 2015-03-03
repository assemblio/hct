from flask import Flask, request, g, url_for, render_template


# URLs
app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
app.add_url_rule('/users/view/', 'user_view', user_view)
app.add_url_rule('/users/create/', 'user_create', user_create)
app.add_url_rule('/logout/', 'logout', logout_view)

# Secret key needed to use sessions.
app.secret_key = 'N4BUdSXUzHxNoO8g'

if __name__ == '__main__':
    app.run(debug=True)
