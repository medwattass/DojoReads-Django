function login_dojoreads()
    {
        loginForm = document.getElementById('loginForm');
        var formData = new FormData(loginForm);
        fetch("/loging_in", { method: 'POST', body: formData })
            .then(response => response.json())
            .then(data => {
                if (data.errors == "success") 
                    {
                        window.location.replace('/books');
                    }
                else 
                    {
                        the_error = document.getElementById('logErrorMessage');
                        the_error.innerHTML = ""
                        for (key in data.errors) {
                            if (the_error.textContent != ""){
                                the_error.innerHTML += "<br>" + data.errors[key];
                            }
                            else{
                                the_error.innerHTML = data.errors[key];
                            }
                        }
                        loginForm.reset();
                    }
            });
    }



function register_dojoreads()
    {
        regForm = document.getElementById('registrationForm');
        var formData = new FormData(regForm);
        fetch("/registring", { method: 'POST', body: formData })
        .then(response => response.json())
        .then(data => 
            {
                if (data.errors == "success") 
                    {
                        window.location.replace('/books/');
                    }
                else 
                    {
                        the_error = document.getElementById('regErrorMessage');
                        the_error.innerHTML = ""
                        for (key in data.errors) {
                            if (the_error.textContent != ""){
                                the_error.innerHTML += "<br>" + data.errors[key];
                            }
                            else{
                                the_error.innerHTML = data.errors[key];
                            }
                        }
                        regForm.reset();
                    }
        });
    }