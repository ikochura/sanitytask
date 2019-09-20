// Call the dataTables jQuery plugin
$(document).ready(function () {
    // $('#dataTable').DataTable();
    $('#dt-day-checks').dataTable({
        "columnDefs": [
            {"orderable": false, "targets": [3, 5]}
        ],
        "language": {
            "emptyTable": "All yesterday task is done"
        }
    });

    $('#dt-today-task').dataTable({
        "columnDefs": [
            {"orderable": false, "targets": [3, 5, 6]}
        ],
        "language": {
            "emptyTable": "There are no tasks today"
        }
    });
});
