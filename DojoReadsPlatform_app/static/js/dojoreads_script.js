function addBook()
    {
        bookForm = document.getElementById('addBookForm');
        var formData = new FormData(bookForm);
        fetch("/books/book/create", { method: 'POST', body: formData })
        .then(response => response.json())
        .then(data => 
            {
                if (data.errors == "success") 
                    {
                        window.location.replace('/books');
                    }
                else 
                    {
                        the_error = document.getElementById('bookErrorMessage');
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

    function addReview()
    {
        bookForm = document.getElementById('addReviewForm');
        var formData = new FormData(bookForm);
        fetch("/books/review/create", { method: 'POST', body: formData })
        .then(response => response.json())
        .then(data => 
            {
                if (data.errors == "success") 
                    {
                        window.location.replace('/books/book/' + data['book_id']);
                    }
                else 
                    {
                        the_error = document.getElementById('reviewErrorMessage');
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