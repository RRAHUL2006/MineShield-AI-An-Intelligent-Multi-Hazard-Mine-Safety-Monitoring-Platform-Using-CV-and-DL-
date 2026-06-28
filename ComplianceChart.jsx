import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement,
    Tooltip,
    Legend
} from "chart.js";

import { Bar, Pie } from "react-chartjs-2";

import "../styles/complianceChart.css";

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement,
    Tooltip,
    Legend
);

export default function ComplianceChart({ statistics }) {

    if (!statistics) return null;

    const labels = [

        "Helmet",
        "Vest",
        "Gloves",
        "Boots",
        "Goggles"

    ];

    const values = [

        statistics.helmet_compliance,

        statistics.vest_compliance,

        statistics.gloves_compliance,

        statistics.boots_compliance,

        statistics.goggles_compliance

    ];

    const chartData = {

    labels: [

        "Helmet",

        "Vest",

        "Gloves",

        "Boots",

        "Goggles"

    ],

    datasets: [

        {

            label: "Compliance (%)",

            data: [

                statistics.helmet_compliance,

                statistics.vest_compliance,

                statistics.gloves_compliance,

                statistics.boots_compliance,

                statistics.goggles_compliance

            ],

            backgroundColor: [

                "#22c55e",   // Green

                "#3b82f6",   // Blue

                "#f59e0b",   // Orange

                "#ef4444",   // Red

                "#8b5cf6"    // Purple

            ],

            borderColor: [

                "#15803d",

                "#1d4ed8",

                "#d97706",

                "#b91c1c",

                "#6d28d9"

            ],

            borderWidth: 2

        }

    ]

};
const options = {

    responsive: true,

    plugins: {

        legend: {

            position: "top"

        }

    },

    scales: {

        y: {

            beginAtZero: true,

            max: 100

        }

    }

};
    return (

        <div className="chart-container">

            <h2>PPE Compliance Analytics</h2>

            <div className="chart-grid">

                <div className="chart-card">

                    <h3>Bar Chart</h3>

                    <Bar
    data={chartData}
    options={options}
/>



                </div>

                <div className="chart-card">

                    <h3>Pie Chart</h3>

                    <Pie
    data={chartData}
/>

                </div>

            </div>

        </div>

    );

}