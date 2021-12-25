const closeLicense = async (id) => {

    // Get the details about the contact again and build the list
    const licensesResults = await fetch(`/get_customer_licenses/${id}`)
    if (!licensesResults.ok) { throw { status: licensesResults.status, statusText: licensesResults.statusText } }
    const licensesData = await licensesResults.json();
    const licenseJsonData = await JSON.parse(licensesData.data)


    let customerLicensesTable = ''
    let licenseEntries = ''

    if (licenseJsonData.length > 0) {
        // With a for loop, add the data fields to a table
        for (i = 0; i < licenseJsonData.length; i++) {
            licenseEntries += `
            <tr id="${licenseJsonData[i].pk}" class="select-customer" onclick="viewLicense(event, '${licenseJsonData[i].pk}')">
                <td>${licenseJsonData[i].fields.product === null ? "" : licenseJsonData[i].fields.product}</td>
                <td>${licenseJsonData[i].fields.purchase_date === null ? "" : licenseJsonData[i].fields.purchase_date}</td>
                <td>${licenseJsonData[i].fields.expiration_date === null ? "" : licenseJsonData[i].fields.expiration_date}</td>
                <td>${licenseJsonData[i].fields.license_key === null ? "" : licenseJsonData[i].fields.license_key}</td>
                <td class="text-truncate"  style="max-width: 50px;">${licenseJsonData[i].fields.license_file === null ? "" : licenseJsonData[i].fields.license_file}</td>
            </tr>
            \n
            `
        }
        customerLicensesTable =
            `
            <!-- CONTACT INFORMATION -->
            <h5 class="text-center baskerville-font mb-3">License Information</h5>
            <table class="table table-striped table-responsive">
                <thead class="thead-dark">
                    <tr>
                        <th scope="col">Product</th>
                        <th scope="col">Purchase Date</th>
                        <th scope="col">Expiration Date</th>
                        <th scope="col">License Key</th>
                        <th scope="col">License File</th>
                    </tr>
                </thead>
                <tbody>
                    ${licenseEntries}
                </tbody>
            </table>
            `
    } else {
        customerLicensesTable = `
        <h5 class="text-center baskerville-font mb-3">License Information</h5>
        No Licenses recorded for this customer.
        `
    }

    // show the div that has the customer's data
    document.querySelector(`#clientDetailsRoot`).style.display = "block"

    // replace the content in the bottom div that has the contact information
    const contactsRoot = document.querySelector(`#contactsDetailsRoot`)
    contactsRoot.style.display = "block"

    // show the licenses again
    const licensesRoot = document.querySelector(`#licensesDetailsRoot`)
    licensesRoot.innerHTML = customerLicensesTable
    licensesRoot.style.display = "block"


    // Hide our old stuff
    const licensesEditRoot = document.querySelector(`#licensesEditContent`)
    licensesEditRoot.innerHTML = ""
    licensesEditRoot.style.display = "none"




}

// Close the small editing form
const cancelLicenseEdit = (fieldName, currentData) => {
    const editButton = document.querySelector(`#edit-license-${fieldName}-icon`)
    editButton.style.display = "block"
    if (currentData && currentData.length > 0) {
        document.querySelector(`#edit-license-${fieldName}`).innerHTML = currentData
    } else {
        document.querySelector(`#edit-license-${fieldName}`).innerHTML = ""
    }

}


const editLicenseField = async (fieldName, id, fieldType) => {
    let editTemplate = "";
    // create the edit form

    // Hide the editing button to fix a bug
    const editButton = document.querySelector(`#edit-license-${fieldName}-icon`)
    editButton.style.display = "none"

    // Get the current data from what is in the inner html
    const currentEditField = document.querySelector(`#edit-license-${fieldName}`)
    const currentData = currentEditField.innerHTML

    // Will have a text field
    if (fieldType === "menu") {
        editTemplate = `
        <form onsubmit="submitEditLicenseForm(event,'${id}', '${fieldName}', 'textInput')">

            <select name="product" class="form-select mb-2" placeholder=""  id="license-input-${fieldName}">
                <option value="AVAST PRO" ${currentData === 'AVAST PRO' ? 'selected' : ""}>AVAST PRO</option>
                <option value="AVAST ENDPOINT" ${currentData === 'AVAST ENDPOINT' ? 'selected' : ""}>AVAST ENDPOINT</option>
                <option value="MALWAREBYTES" ${currentData === 'MALWAREBYTES' ? 'selected' : ""}>MALWAREBYTES</option>
                <option value="MICROSOFT OFFICE 2010" ${currentData === 'MICROSOFT OFFICE 2010' ? 'selected' : ""}>MICROSOFT OFFICE 2010</option>
                <option value="MICROSOFT OFFICE 2013" ${currentData === 'MICROSOFT OFFICE 2013' ? 'selected' : ""}>MICROSOFT OFFICE 2013</option>
                <option value="MICROSOFT OFFICE 2016" ${currentData === 'MICROSOFT OFFICE 2016' ? 'selected' : ""}>MICROSOFT OFFICE 2016</option>
                <option value="MICROSOFT OFFICE 2019" ${currentData === 'MICROSOFT OFFICE 2019' ? 'selected' : ""}>MICROSOFT OFFICE 2019</option>
                <option value="MICROSOFT OFFICE 365" ${currentData === 'MICROSOFT OFFICE 365' ? 'selected' : ""}>MICROSOFT OFFICE 365</option>
            </select> 
            <div class="float-end">
                <button class="btn btn-sm btn-logo" type="submit">Save</button>
                <button class="btn btn-sm btn-silver" type="button" onclick="cancelLicenseEdit('${fieldName}', '${currentData}' )">Cancel</button>
            </div>
        </form>
        `
    }

    // a textarea
    if (fieldType === "textarea") {
        editTemplate = `
        <form onsubmit="submitEditLicenseForm(event,'${id}', '${fieldName}', 'textarea')">
            <textarea class="form-control mb-2 form-control-sm" id="license-input-${fieldName}">${currentData === 'null' ? "" : currentData}</textarea>
            <div class="float-end">
                <button class="btn btn-sm btn-logo" type="submit">Save</button>
                <button class="btn btn-sm btn-silver" type="button" onclick="cancelLicenseEdit('${fieldName}', '${currentData}' )">Cancel</button>
            </div>
        </form>
        `
    }

    // a date field
    if (fieldType === "date") {
        editTemplate = `
        <form onsubmit="submitEditLicenseForm(event,'${id}', '${fieldName}', 'date')">
            <input type="date" class="form-control mb-2 form-control-sm" id="license-input-${fieldName}" value='${currentData === 'null' ? "" : currentData}'>
            <div class="float-end">
                <button class="btn btn-sm btn-logo" type="submit">Save</button>
                <button class="btn btn-sm btn-silver" type="button" onclick="cancelLicenseEdit('${fieldName}', '${currentData}' )">Cancel</button>
            </div>
        </form>
        `
    }

    // and a file field
    if (fieldType === "file") {
        editTemplate = `
        <form onsubmit="submitEditLicenseForm(event,'${id}', '${fieldName}', 'file')">
            <input type="file" class="form-control mb-2 form-control-sm" id="license-input-${fieldName}">
            <div class="float-end">
                <button class="btn btn-sm btn-logo" type="submit">Save</button>
                <button class="btn btn-sm btn-silver" type="button" onclick="cancelLicenseEdit('${fieldName}')">Cancel</button>
            </div>
        </form>
        `
    }

    // insert the form into the div
    currentEditField.innerHTML = editTemplate
}






const submitEditLicenseForm = async (event, id, fieldName, fieldType) => {
    event.preventDefault() // stop any propegation

    // Get the data from the form
    const data = document.querySelector(`#license-input-${fieldName}`)
    const submission = {
        [fieldName]: data.value // use [] for a json key variable
    }

    try {

        // Send the data to the back end
        const results = await fetch(`/edit_license/${id}/${fieldName}`, {
            method: "POST",
            body: JSON.stringify(submission),
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        console.log(results)
        console.log(submission)
    }
    catch (error) {

    }

}