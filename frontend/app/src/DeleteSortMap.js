import React, { useState } from 'react';

function DeleteSortMap({ deleteSortMap , resetState}) {
  const [id, setId] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    await resetState();
    await deleteSortMap(id);
    setId('');
  };

  return (
    <div className="card bg-dark text-white">
      <div className="card-header">Delete SortMap</div>
      <div className="card-body">
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="sortmap-id" className="form-label">
              SortMap Id:
            </label>
            <input
              type="text"
              className="form-control"
              id="sortmap-id"
              value={id}
              onChange={(e) => setId(e.target.value)}
            />
          </div>
          <button type="submit" className="btn btn-primary">
            Delete a SortMap
          </button>
        </form>
      </div>
    </div>
  );
}

export default DeleteSortMap;
