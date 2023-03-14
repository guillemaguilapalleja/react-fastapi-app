import React, { useState } from 'react';

function GetSortMapById({ getSortMapById, resetState }) {
  const [id, setId] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    await resetState();
    getSortMapById(id);
    setId('');
  };

  return (
    <div className="card bg-dark text-white">
      <div className="card-header">Get SortMap By Id</div>
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
            Get SortMap By Id
          </button>
        </form>
      </div>
    </div>
  );
}

export default GetSortMapById;
