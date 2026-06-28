import "../styles/complianceOverview.css";

export default function ComplianceOverview({ statistics }) {

    if (!statistics) return null;

    const items = [

        {
            name: "Helmet",
            value: statistics.helmet_compliance
        },

        {
            name: "Vest",
            value: statistics.vest_compliance
        },

        {
            name: "Gloves",
            value: statistics.gloves_compliance
        },

        {
            name: "Boots",
            value: statistics.boots_compliance
        },

        {
            name: "Goggles",
            value: statistics.goggles_compliance
        }

    ];

    return (

        <div className="compliance-overview">

            <h2>PPE Compliance Overview</h2>

            {

                items.map((item) => (

                    <div
                        className="compliance-row"
                        key={item.name}
                    >

                        <span>

                            {item.name}

                        </span>

                        <div className="progress-container">

                            <div

                                className="progress-fill"

                                style={{

                                    width: `${item.value}%`

                                }}

                            />

                        </div>

                        <span>

                            {item.value}%

                        </span>

                    </div>

                ))

            }

        </div>

    );

}