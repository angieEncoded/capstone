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
            <textarea class="form-control mb-2 form-control-sm" id="input-${fieldName}">${currentData}</textarea>
            <div class="float-end">
            <button class="btn btn-sm btn-logo" type="submit">Save</button>
            <button class="btn btn-sm btn-silver" type="button" onclick="cancelEdit('${fieldName}', '${currentData}' )">Cancel</button>
            </div>
        </form>
        `
    } else {
        editTemplate = `
        <form onsubmit="submitForm(event,'${id}', '${fieldName}')">
            <input type="text" class="form-control mb-2 form-control-sm" value='${currentData}' id="input-${fieldName}" maxlength=255 />
            <div class="float-end">
            <button class="btn btn-sm btn-logo" type="submit">Save</button>
            <button class="btn btn-sm btn-silver" type="button" onclick="cancelEdit('${fieldName}', '${currentData}' )">Cancel</button>
            </div>
        </form>
        `
    }


    currentEditField.innerHTML = editTemplate
}