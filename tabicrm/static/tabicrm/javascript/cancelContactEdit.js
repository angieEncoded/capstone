
// Close the small editing form
const cancelContactEdit = (fieldName, currentData) => {
    const editButton = document.querySelector(`#edit-contact-${fieldName}-icon`)
    editButton.style.display = "block"
    document.querySelector(`#edit-contact-${fieldName}`).innerHTML = currentData
}