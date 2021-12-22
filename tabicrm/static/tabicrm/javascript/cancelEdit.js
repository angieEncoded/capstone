// Close the small editing form
const cancelEdit = (fieldName, currentData) => {
    const editButton = document.querySelector(`#edit-${fieldName}-icon`)
    editButton.style.display = "block"
    document.querySelector(`#edit-${fieldName}`).innerHTML = currentData
}