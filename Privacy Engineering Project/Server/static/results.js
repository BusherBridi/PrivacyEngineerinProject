document.addEventListener("DOMContentLoaded", function () {
    // Get the tables
    var employeesTable = document.getElementById("employeesTable");
    var reportsTable = document.getElementById("reportsTable");

    // Add click event listener to the employees table
    employeesTable.addEventListener("click", function (event) {
        handleRowClick(event, employeesTable);
    });

    // Function to handle row clicks for the employees table
    function handleRowClick(event, table) {
        var target = event.target;

        // Check if the clicked element is a table cell
        if (target.tagName === "TD") {
            // Remove existing selection
            var selectedRows = table.querySelectorAll("tbody tr.selected");
            selectedRows.forEach(function (row) {
                row.classList.remove("selected");
            });

            // Get the clicked row
            var currentRow = target.parentNode;

            // Add a class to highlight the selected row
            currentRow.classList.add("selected");

            // Get the row data
            var rowData = [];
            var cells = currentRow.getElementsByTagName("td");

            for (var i = 0; i < cells.length; i++) {
                rowData.push(cells[i].innerText);
            }

            // Log the rowData to the console (replace with your actual logic)
            console.log("Selected Row Data (Employees):", rowData);

            // Access data from the Reports table (call the function)
            var reportsData = getReportsTableData();
            console.log("Data from Reports Table:", reportsData);
        }
    }

    // Function to get data from the Reports table
    function getReportsTableData() {
        var reportsData = [];
        var rows = reportsTable.querySelectorAll("tbody tr");

        rows.forEach(function (row) {
            var rowData = [];
            var cells = row.getElementsByTagName("td");

            for (var i = 0; i < cells.length; i++) {
                rowData.push(cells[i].innerText);
            }

            reportsData.push(rowData);
        });
        return reportsData;
    }
});
