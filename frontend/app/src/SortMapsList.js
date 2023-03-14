import React from 'react';

function SortMapsList({ getSortmaps, resetState, sortMaps }) {
  const handleSubmit = async (e) => {
    e.preventDefault();
    await resetState();
    await getSortmaps();
  };

  return (
    <div className="card bg-dark text-white">
      <div className="card-header">Get List of SortMaps</div>
      <div className="card-body">
        <form onSubmit={handleSubmit}>
          <button type="submit" className="btn btn-primary">Get SortMaps</button>
        </form>
        {sortMaps && sortMaps.map((map, index) => (
          <div key={index} className="border-bottom mb-3">
            <pre>{JSON.stringify(map, null, 2)}</pre>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SortMapsList;
