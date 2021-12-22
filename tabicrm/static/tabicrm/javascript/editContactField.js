
const editContactField = async (fieldName, id, fieldType) => {
    let editTemplate = "";
    // create the edit form

    // Hide the editing button to fix a bug
    const editButton = document.querySelector(`#edit-contact-${fieldName}-icon`)
    editButton.style.display = "none"

    // GEt the current data from what is in the inner html
    const currentEditField = document.querySelector(`#edit-contact-${fieldName}`)
    const currentData = currentEditField.innerHTML



    if (fieldType === "textarea") {
        editTemplate = `
        <form onsubmit="submitEditContactForm(event,'${id}', '${fieldName}')">
            <textarea class="form-control mb-2 form-control-sm" id="contact-input-${fieldName}">${currentData === 'null' ? "" : currentData}</textarea>
            <div class="float-end">
            <button class="btn btn-sm btn-logo" type="submit">Save</button>
            <button class="btn btn-sm btn-silver" type="button" onclick="cancelContactEdit('${fieldName}', '${currentData}' )">Cancel</button>
            </div>
        </form>
        `
    } else {
        editTemplate = `
        <form onsubmit="submitEditContactForm(event,'${id}', '${fieldName}')">
            <input type="text" class="form-control mb-2 form-control-sm" value='${currentData === 'null' ? "" : currentData}' id="contact-input-${fieldName}" maxlength=255 />
            <div class="float-end">
            <button class="btn btn-sm btn-logo" type="submit">Save</button>
            <button class="btn btn-sm btn-silver" type="button" onclick="cancelContactEdit('${fieldName}', '${currentData}' )">Cancel</button>
            </div>
        </form>
        `
    }

    // insert the form into the div
    currentEditField.innerHTML = editTemplate
}
