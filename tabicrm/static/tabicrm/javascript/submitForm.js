

const submitForm = async (event, id, fieldName) => {
    event.preventDefault() // stop any propegation

    // Get the data from the form
    const data = document.querySelector(`#input-${fieldName}`)
    const submission = {
        [fieldName]: data.value // use [] for a json key variable
    }

    try {
        // Send the request to the back end to update the data
        const results = await fetch(`/edit_customer/${id}/${fieldName}`, {
            method: "POST",
            body: JSON.stringify(submission),
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        if (!results.ok) { throw { status: results.status, statusText: results.statusText } }
        const data = await results.json()

        // If the server sent back an error because we did something wrong
        if (data.error) { throw data.error }

        if (data.success) {
            const successDiv = document.querySelector(`#customer-feedback-data`)
            successDiv.innerHTML = `<span class="text-success">${data.success}</span>`
            document.querySelector(`#edit-${fieldName}`).innerHTML = data.content
            // Hide the editing button to fix a bug
            const editButton = document.querySelector(`#edit-${fieldName}-icon`)
            editButton.style.display = "block"
            setTimeout(() => {
                successDiv.innerHTML = ""
            }, 10000);
        }
    } catch (error) {
        console.log(error)
        const errorDiv = document.querySelector(`#customer-feedback-data`)
        if (error.status) {
            errorDiv.innerHTML = `<span class="text-danger">${error.status} ${error.statusText}</span>`
        } else {
            errorDiv.innerHTML = `<span class="text-danger">${error}</span>`
        }
        setTimeout(() => {
            errorDiv.innerHTML = ""
        }, 20000);
    }



}