const showConfirmDeleteModal = () => {
    // create the modal
    let confirmModal = new bootstrap.Modal(document.getElementById('confirmDelete'), {
        keyboard: false,
        backdrop: 'static'
    })
    confirmModal.show()
}