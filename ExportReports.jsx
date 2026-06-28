import {

    exportCSV,

    exportExcel,

    exportPDF

}

from "../services/api";
export default function ExportReports() {

    return (

        <div className="export-container">

            <h2>Export Reports</h2>

            <div className="export-buttons">

                <button

    className="pdf-btn"

    onClick={exportPDF}

>

    📄 Export PDF

</button>

                <button

    className="excel-btn"

    onClick={exportExcel}

>

    📊 Export Excel

</button>

                <button

                    className="csv-btn"

                    onClick={exportCSV}

                >

                    📋 Export CSV

                </button>

            </div>

        </div>

    );

}