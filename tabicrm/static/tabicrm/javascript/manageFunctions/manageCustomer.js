


const editField = async (fieldName, id, fieldType) => {

    // Hide the editing button to fix a bug
    const editButton = document.querySelector(`#edit-${fieldName}-icon`)
    editButton.style.display = "none"

    // GEt the current data from what is in the inner html
    const currentEditField = document.querySelector(`#edit-${fieldName}`)
    const currentData = currentEditField.innerHTML

    let editTemplate;
    // create the edit form
    if (fieldType === "textarea") {
        editTemplate = `
        <form onsubmit="submitForm(event,'${id}', '${fieldName}')">
            <textarea class="form-control mb-2 form-control-sm" id="input-${fieldName}">${currentData === 'null' ? "" : currentData.trim()}</textarea>
            <div class="float-end">
            <button class="btn btn-sm btn-logo" type="submit">Save</button>
            <button class="btn btn-sm btn-silver" type="button" onclick="cancelEdit('${fieldName}', '${currentData}' )">Cancel</button>
            </div>
        </form>
        `
    } else {
        editTemplate = `
        <form onsubmit="submitForm(event,'${id}', '${fieldName}')">
            <input type="text" class="form-control mb-2 form-control-sm" value='${currentData === 'null' ? "" : currentData.trim()}' id="input-${fieldName}" maxlength=255 />
            <div class="float-end">
            <button class="btn btn-sm btn-logo" type="submit">Save</button>
            <button class="btn btn-sm btn-silver" type="button" onclick="cancelEdit('${fieldName}', '${currentData}' )">Cancel</button>
            </div>
        </form>
        `
    }


    currentEditField.innerHTML = editTemplate
}

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

// Close the small editing form
const cancelEdit = (fieldName, currentData) => {
    const editButton = document.querySelector(`#edit-${fieldName}-icon`)
    editButton.style.display = "block"
    document.querySelector(`#edit-${fieldName}`).innerHTML = currentData
}