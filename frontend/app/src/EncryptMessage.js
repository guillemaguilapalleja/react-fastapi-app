import React, { useState } from 'react';

function EncryptMessage({ encryptMessage, resetState }) {
  const [id, setId] = useState('');
  const [value, setValue] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    await resetState();
    encryptMessage(id, value);
    setId('');
    setValue('');
  };

  return (
    <div className="card bg-dark text-white">
      <div className="card-header">Encrypt a message</div>
      <div className="card-body">
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="sortmap-id" className="form-label">
              SortMap ID
            </label>
            <input
              type="text"
              className="form-control"
              id="sortmap-id"
              value={id}
              onChange={(event) => setId(event.target.value)}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="sortmap-value" className="form-label">
              Message to encrypt
            </label>
            <input
              type="text"
              className="form-control"
              id="sortmap-value"
              value={value}
              onChange={(event) => setValue(event.target.value)}
            />
          </div>
          <button type="submit" className="btn btn-primary">
            Encrypt message
          </button>
        </form>
      </div>
    </div>
  );
}

export default EncryptMessage;
