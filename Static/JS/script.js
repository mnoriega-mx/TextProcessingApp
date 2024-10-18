$(document).ready(function() {
    let file1Content = null;
    let file2Content = null;

    // Autocomplete functionality
    $('#autocomplete').on('input', function() {
        var prefix = $(this).val();
        if (prefix.length > 0) {
            $.get('/autocomplete', { prefix: prefix }, function(data) {
                $('#suggestions').empty();
                data.forEach(function(suggestion) {
                    $('#suggestions').append('<li>' + suggestion + '</li>');
                });
            });
        } else {
            $('#suggestions').empty();
        }
    });

    // Trigger file1 input on button click
    document.getElementById('file1-button').addEventListener('click', function() {
        document.getElementById('file1').click();
    });

    // Trigger file2 input on button click
    document.getElementById('file2-button').addEventListener('click', function() {
        document.getElementById('file2').click();
    });

    // Display content of file1 and store it
    document.getElementById('file1').addEventListener('change', function() {
        var file = this.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function(e) {
                file1Content = e.target.result;
                console.log("File 1 content:", file1Content); // Log to check if the content is being set
                document.querySelector('.text-display:nth-child(1) pre').textContent = file1Content;
                document.getElementById('file1-hidden').value = file1Content;
            }
            reader.readAsText(file);
        }
    });

    // Display content of file2 and store it
    let originalText2 = null;  // Store the original text2
    document.getElementById('file2').addEventListener('change', function() {
        var file = this.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function(e) {
                file2Content = e.target.result;
                originalText2 = file2Content;  // Store the original text when file is loaded
                document.querySelector('.text-display:nth-child(2) pre').textContent = file2Content;
            }
            reader.readAsText(file);
        }
    });


    // Handle form submission via AJAX
    $('form').submit(function(event) {
        event.preventDefault();  // Prevent page refresh
        let algorithm = $(this).find('button[type=submit][clicked=true]').val();
        
        // Log the file content to ensure it's being sent
        console.log("Sending file1Content:", file1Content);
        console.log("Sending file2Content:", file2Content);

        // Send data via AJAX instead of traditional form submission
        $.ajax({
            type: 'POST',
            url: '/process',
            data: {
                file1Content: file1Content,  // Make sure this is not null or empty
                file2Content: file2Content,
                algorithm: algorithm,
                pattern: $('#pattern').val(),
                autocomplete: $('#autocomplete').val()
            },
            success: function(response) {
                console.log("Response from server:", response);  // Log server response
            
                // If the algorithm is "KMP" or "Palindrome", highlight text in the original display
                if (response.algorithm === "KMP" || response.algorithm === "Palindrome") {
                    $('.text-display:nth-child(1) pre').html(response.result);  // Update the first text display with highlighted result for KMP/Palindrome
                    $('.text-display:nth-child(2) pre').html(originalText2);  // Restore the original text2 (remove LCS highlights)
                } else if (response.algorithm === "LCS") {
                    // Update both text displays with the highlighted LCS result
                    $('.text-display:nth-child(1) pre').html(response.text1);  // Highlighted version of text1
                    $('.text-display:nth-child(2) pre').html(response.text2);  // Highlighted version of text2
                } else {
                    // Default case: show the result in the result display area
                    $('.result-display pre').html(response.result); 
                }
            },                                 
            error: function(xhr, status, error) {
                console.error("Error processing request:", xhr.responseText);  // Log the error response
            }
        });
    });

    // Track which button was clicked to identify the algorithm
    $('button[type=submit]').click(function() {
        $('button[type=submit]', $(this).parents('form')).removeAttr('clicked');
        $(this).attr('clicked', 'true');
    });
});