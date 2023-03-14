import React, { useState } from 'react';

function CreateSortMap({ createSortMap, resetState }) {
  const [value, setValue] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    await resetState();
    await createSortMap(value);
    setValue('');
  };

  return (
    <div className="card bg-dark text-white">
      <div className="card-header">Create a new SortMap</div>
      <div className="card-body">
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="value" className="form-label">
              Value
            </label>
            <input
              type="text"
              className="form-control"
              id="value"
              value={value}
              onChange={(e) => setValue(e.target.value)}
            />
          </div>
          <button type="submit" className="btn btn-primary">
            Create
          </button>
        </form>
      </div>
    </div>
  );
}

export default CreateSortMap;
