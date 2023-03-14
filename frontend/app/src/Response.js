import React from "react";

function Response({ data, title }) {
  const responseObj = Array.isArray(data) ? data : [JSON.parse(data)];

   return (
    <div className="card bg-dark mb-3 text-white">
      <div className="card-header">{title}</div>
      <div className="card-body">
        {responseObj.map((response, index) => (
          <ul key={index} style={{ listStyle: 'none', textAlign: 'center' }}>
            {Object.entries(response).map(([key, value]) => (
              <li key={key}>
                <strong>{key}:</strong> {value}
              </li>
            ))}
          </ul>
        ))}
      </div>
    </div>
  );
}

export default Response;
