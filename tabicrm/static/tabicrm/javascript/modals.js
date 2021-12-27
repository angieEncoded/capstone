const showConfirmDeleteModal = () => {
    // create the modal
    let confirmModal = new bootstrap.Modal(document.getElementById('confirmDelete'), {
        keyboard: false,
        backdrop: 'static'
    })
    confirmModal.show()
}

const showNewContactFormModal = () => {
    let newContactModal = new bootstrap.Modal(document.getElementById('addContactModal'), {
        keyboard: false,
        backdrop: 'static'
    })
    newContactModal.show()
}

const showNewLicenseFormModal = () => {
    let newContactModal = new bootstrap.Modal(document.getElementById('addLicenseModal'), {
        keyboard: false,
        backdrop: 'static'
    })
    newContactModal.show()
}

const showNewEquipmentFormModal = () => {
    let newEquipmentModal = new bootstrap.Modal(document.getElementById('addEquipmentModal'), {
        keyboard: false,
        backdrop: 'static'
    })
    newEquipmentModal.show()
}