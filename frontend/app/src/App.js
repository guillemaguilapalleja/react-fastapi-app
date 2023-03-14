import React, { useState } from 'react';
import SortMapsList from './SortMapsList';
import CreateSortMap from './CreateSortMap';
import GetSortMapById from "./GetSortMap";
import UpdateSortMap from "./UpdateSortMap";
import DeleteSortMap from "./DeleteSortMap";
import EncryptMessage from "./EncryptMessage";
import Response from "./Response";
import 'bootstrap/dist/css/bootstrap.min.css';


function App() {
  const [sortmapsResponse, setSortmapsResponse] = useState("");
  const [createSortMapResponse, setCreateSortMapResponse] = useState("");
  const [getSortMapByIdResponse, setGetSortMapByIdResponse] = useState("");
  const [updateSortMapResponse, setUpdateSortMapResponse] = useState("");
  const [deleteSortMapResponse, setDeleteSortMapResponse] = useState("");
  const [encryptMessageResponse, setEncryptMessageResponse] = useState("");

  const resetState = async () => {
    setSortmapsResponse("");
    setCreateSortMapResponse("");
    setGetSortMapByIdResponse("");
    setUpdateSortMapResponse("");
    setDeleteSortMapResponse("");
    setEncryptMessageResponse("");
  }

  const getSortmaps = async () => {
    const response = await fetch('http://localhost:8080/api/sortmaps_list', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const data = await response.json();
    if (data.hasOwnProperty("detail") === true) {
      data["ERROR"] = data["detail"]
      delete data["detail"]
    }
    setSortmapsResponse(data);
  };

  const createSortMap = async (value) => {
    const response = await fetch('http://localhost:8080/api/sortmap', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ value }),
    });
    const data = await response.json();
    if (data.hasOwnProperty("detail") === true) {
      data["ERROR"] = data["detail"]
      delete data["detail"]
    }
    setCreateSortMapResponse(JSON.stringify(data));
  };

  const getSortMapById = async (id) => {
    const response = await fetch(`http://localhost:8080/api/sortmaps?sortmap_id=${id}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const data = await response.json();
    if (data.hasOwnProperty("detail") === true) {
      data["ERROR"] = data["detail"]
      delete data["detail"]
    }
    setGetSortMapByIdResponse(JSON.stringify(data));
  };

  const updateSortMap = async (id, value) => {
    const response = await fetch(`http://localhost:8080/api/sortmap/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ value }),
    });
    const data = await response.json()
    if (data.hasOwnProperty("detail") === true) {
      data["ERROR"] = data["detail"]
      delete data["detail"]
    }
    setUpdateSortMapResponse(JSON.stringify(data));
  };

  const deleteSortMap = async (id) => {
    await fetch(`http://localhost:8080/api/sortmap/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    setDeleteSortMapResponse(`SortMap with ID ${id} deleted`);
  };

  const encryptMessage = async (id, message) => {
    const response = await fetch(`http://localhost:8080/api/order?sortmap_id=${id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ "request": message }),
    });
    const data = await response.json();
    if (data.hasOwnProperty("detail") === true) {
      data["ERROR"] = data["detail"]
      delete data["detail"]
    }
    setEncryptMessageResponse(JSON.stringify(data));
  };

return (
    <div className="container py-5">
      <div className="row flex-column">
        <div className="col mb-2">
          <button type="submit" className="btn btn-primary w-100" onClick={resetState}>
            Reset
          </button>
        </div>
        <div className="col mb-2">
            <div className="card-body">
              <SortMapsList getSortmaps={getSortmaps} resetState={resetState}/>
              {sortmapsResponse && <Response title="SortMaps" data={sortmapsResponse} />}
            </div>
        </div>
        <div className="col mb-2">
            <div className="card-body">
              <CreateSortMap createSortMap={createSortMap} resetState={resetState}/>
              {createSortMapResponse && <Response title="New SortMap" data={createSortMapResponse} />}
            </div>
        </div>
        <div className="col mb-2">
          <div className="card-body">
            <GetSortMapById getSortMapById={getSortMapById} resetState={resetState}/>
            {getSortMapByIdResponse && <Response title="SortMap information" data={getSortMapByIdResponse} />}
          </div>
        </div>
        <div className="col mb-2">
          <div className="card-body">
            <UpdateSortMap updateSortMap={updateSortMap} resetState={resetState}/>
            {updateSortMapResponse && <Response title="SortMap updated" data={updateSortMapResponse} />}
          </div>
        </div>
        <div className="col mb-2">
          <div className="card-body">
            <DeleteSortMap deleteSortMap={deleteSortMap} resetState={resetState}/>
            {deleteSortMapResponse && <Response title="SortMap deleted" data={deleteSortMapResponse} />}
          </div>
        </div>
        <div className="col mb-2">
          <div className="card-body">
            <EncryptMessage encryptMessage={encryptMessage} resetState={resetState}/>
            {encryptMessageResponse && <Response title="Message encrypted information" data={encryptMessageResponse} />}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
