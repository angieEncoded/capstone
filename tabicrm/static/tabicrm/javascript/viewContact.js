const viewContact = async (event, id) => {
    // hide the div that has the customer's data
    document.querySelector(`#clientDetailsRoot`).style.display = "none"
    document.querySelector(`#contactsDetailsRoot`).style.display = "none"

    // get the div that we want to display our data in
    const contactsRoot = document.querySelector(`#contactsEditContent`)

    try {

        // Get the data for the contact
        const contactResults = await fetch(`/get_contact/${id}`)
        if (!contactResults.ok) { throw { status: contactResults.status, statusText: contactResults.statusText } }
        const contactData = await contactResults.json();
        const contactJsonData = await JSON.parse(contactData.data)
        const finalContactData = contactJsonData[0].fields
        const contactId = contactJsonData[0].pk
        // populate the form
        const contactDetails = `
            <div class="container-fluid">
                <h5 class="text-center baskerville-font mb-3">Contact Information</h5>
                <div class="row">
                    <div class="col-12 col-xl-6">
                        <div class="row mb-2">
                            <div class="col-4 d-none d-lg-block">First Name: </div>
                            <div class="col-10 col-lg-4"><div id="edit-contact-first_name">${finalContactData.first_name === null ? "" : finalContactData.first_name}</div></div>
                            <div class="col-2 col-lg-4"><i id="edit-contact-first_name-icon" class="las la-edit icon-hover" onclick="editContactField('first_name', '${contactId}', 'textinput')"></i></div>
                        </div>
                        <div class="row mb-2">
                            <div class="col-4 d-none d-lg-block">Last Name: </div>
                            <div class="col-10 col-lg-4"><div id="edit-contact-last_name">${finalContactData.last_name === null ? "" : finalContactData.last_name}</div></div>
                            <div class="col-2 col-lg-4"><i id="edit-contact-last_name-icon"  class="las la-edit icon-hover" onclick="editContactField('last_name', '${contactId}', 'textinput')"></i></div>
                        </div>
                        <div class="row mb-2">
                            <div class="col-4 d-none d-lg-block">Job Title: </div>
                            <div class="col-10 col-lg-4"><div id="edit-contact-job_title">${finalContactData.job_title === null ? "" : finalContactData.job_title} </div></div>
                            <div class="col-2 col-lg-4"><i id="edit-contact-job_title-icon"  class="las la-edit icon-hover" onclick="editContactField('job_title', '${contactId}',  'textinput')"></i></div>
                        </div>
                    </div>
                    <div class="col-12 col-xl-6">
                        <div class="row mb-2">
                            <div class="col-4 d-none d-lg-block">Extension: </div>
                            <div class="col-10 col-lg-4"><div id="edit-contact-extension">${finalContactData.extension === null ? "" : finalContactData.extension} </div></div>
                            <div class="col-2 col-lg-4"><i id="edit-contact-extension-icon"  class="las la-edit icon-hover" onclick="editContactField('extension', '${contactId}',  'textinput')"></i></div>
                        </div>
                        <div class="row mb-2">
                            <div class="col-4 d-none d-lg-block">Notes</div>
                            <div class="col-10 col-lg-4"><div id="edit-contact-notes">${finalContactData.notes === null ? "" : finalContactData.notes}</div></div>
                            <div class="col-2 col-lg-4"><i id="edit-contact-notes-icon"  class="las la-edit icon-hover" onclick="editContactField('notes', '${contactId}', 'textarea')"></i></div>
                        </div>
                    </div>
                </div>
            </div>
            <hr>
            <div class="float-end">
                <button class="btn btn-sm btn-silver" type="button" onclick="closeContact('${finalContactData.assigned_to}')">Back to client</button>
            </div>
        
        `
        // unhide the html root and add the data to ir
        contactsRoot.style.display = "block"
        contactsRoot.innerHTML = contactDetails


    } catch (error) {
        console.log(error)
        const errorDiv = document.querySelector(`#customer-feedback-data`)
        if (error.status) {
            errorDiv.innerHTML = `<span class="text-danger">${error.status} ${error.statusText}</span>`
        } else {
            errorDiv.innerHTML = `<span class="text-danger">${error}</span>`
        }
    }
}