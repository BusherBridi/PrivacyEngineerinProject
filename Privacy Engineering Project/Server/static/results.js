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
            SelectedEmployeeQuasiIdentifiers = rowData.slice(2);
            console.log("Quasiidneftier employee selected:", SelectedEmployeeQuasiIdentifiers);



            // Access data from the Reports table (call the function)
            var reportsData = getReportsTableData();
            var reportsDataQI = []
            for (var i = 0; i < reportsData.length; i++) {
                var slicedData = reportsData[i].slice(1, 5)
                reportsDataQI.push(slicedData)
            }

            var employeeQI = getEmployeesTableDataQI();
            console.log("Data from Reports Table:", reportsData);
            console.log(" EMPLOYEE QI:", employeeQI);
            // var reportsDataQI = getReportsTableDataQI();
            console.log("REPORTS QI:", reportsDataQI);
            console.log("Employee Quasi Count:", countArrayOccurrences(employeeQI, SelectedEmployeeQuasiIdentifiers))
            var deltaPresenceEmployeeCount = countArrayOccurrences(employeeQI, SelectedEmployeeQuasiIdentifiers);
            var deltaPresenceReportCount = countArrayOccurrences(reportsDataQI, SelectedEmployeeQuasiIdentifiers)
            var deltaPresence = deltaPresenceEmployeeCount / deltaPresenceReportCount;
            console.log("Delta Presence of selcted person:", deltaPresence);
            var deltaPresenceElement = document.getElementById("deltaPresenceResult");
            deltaPresenceElement.innerHTML = deltaPresence;
            deltaPresenceElement.style.color = "blue";

        }
    }
    function countArrayOccurrences(arrayOfArrays, givenArray) {
        return arrayOfArrays.reduce((acc, innerArray) => {
            const isEqual = innerArray.every((element, index) => element === givenArray[index]);
            return acc + (isEqual ? 1 : 0);
        }, 0);
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

    function getReportsTableDataQI() {
        var reportsData = [];
        var rows = reportsTable.querySelectorAll("tbody tr");

        rows.forEach(function (row) {
            var rowData = [];
            var cells = row.getElementsByTagName("td");

            // Define the indices of the columns you want to store
            var columnIndices = [1, 2, 3, 4]; // Adjust these indices based on your requirements

            for (var i = 0; i < columnIndices.length; i++) {
                var columnIndex = columnIndices[i];
                rowData.push(cells[columnIndex].innerText);
            }

            reportsData.push(rowData);
        });

        return reportsData;
    }

    function getEmployeesTableData() {
        var employeeData = [];
        var rows = employeesTable.querySelectorAll("tbody tr");

        rows.forEach(function (row) {
            var rowData = [];
            var cells = row.getElementsByTagName("td");

            for (var i = 0; i < cells.length; i++) {
                rowData.push(cells[i].innerText);
            }

            employeeData.push(rowData);
        });
        return employeeData;
    }

    function getEmployeesTableDataQI() {
        var employeeData = [];
        var rows = employeesTable.querySelectorAll("tbody tr");

        rows.forEach(function (row) {
            var rowData = [];
            var cells = row.getElementsByTagName("td");

            // Define the indices of the columns you want to store
            var columnIndices = [2, 3, 4, 5]; // Adjust these indices based on your requirements

            for (var i = 0; i < columnIndices.length; i++) {
                var columnIndex = columnIndices[i];
                rowData.push(cells[columnIndex].innerText);
            }

            employeeData.push(rowData);
        });

        return employeeData;
    }
});
