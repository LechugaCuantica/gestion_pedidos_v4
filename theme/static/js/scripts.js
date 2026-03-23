function onDelete(id, app) {
    let txt = "";
    switch (app) {
        case 'pedidos':
            txt = "Estás seguro de eliminar el pedido?";
            break;
        case 'productos':
            txt = "Estás seguro de eliminar el producto?";
            break;
        case 'clientes':
            txt = "Estás seguro de eliminar el cliente?";
            break;
        default:
            return alert("app no válida.")
    }

    Swal.fire({
        title: txt,
        text: "Esta acción no se puede revertir",
        icon: "warning",
        showCancelButton: true,
        background: "#f8f9fa",
        confirmButtonColor: "#f56565",
        cancelButtonColor: "#c6c9cb",
        confirmButtonText: "Si, eliminar",
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`http://127.0.0.1:8000/${app}/eliminar/${id}`)
                .then((response) => {
                    if (response.status == 400) {
                        return response.json().then(err => {
                            throw err;
                        });
                    }
                    return response.json();
                })
                .then((data) => {
                    let timerInterval;
                    Swal.fire({
                        title: `${data.msg}`,
                        timer: 2000,
                        icon: "success",
                        timerProgressBar: true,
                        showConfirmButton: false,
                        willClose: () => {
                            clearInterval(timerInterval);
                        }
                    }).then((result) => {
                        window.location.reload()
                    });
                }).catch((err) => {
                    let timerInterval;
                    Swal.fire({
                        title: `${err.msg}`,
                        timer: 3000,
                        icon: "error",
                        timerProgressBar: true,
                        showConfirmButton: false,
                        willClose: () => {
                            clearInterval(timerInterval);
                        }
                    }).then((result) => {

                    })
                })
        }
    });
}