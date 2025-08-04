import React, { useEffect, useState } from "react";
import axios from "axios";
import "./CustomerList.css";

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [searchText, setSearchText] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const res = await axios.get("http://localhost:5000/customers");
        setCustomers(res.data);
        setFiltered(res.data);
        setLoading(false);
      } catch (err) {
        console.error("Error:", err);
        setError("Failed to load customer data.");
        setLoading(false);
      }
    };

    fetchCustomers();
  }, []);

  useEffect(() => {
    const term = searchText.trim().toLowerCase();

    if (!term) {
      setFiltered(customers);
      return;
    }

    const results = customers.filter((cust) => {
      const fullName = `${cust.first_name} ${cust.last_name}`.toLowerCase();
      const email = cust.email.toLowerCase();
      return fullName.includes(term) || email.includes(term);
    });

    setFiltered(results);
  }, [searchText, customers]);

  if (loading) return <p className="status-message">Loading customers...</p>;
  if (error) return <p className="status-message error">{error}</p>;

  return (
    <div className="customer-wrapper">
      <div className="search-container">
        <input
          type="text"
          placeholder="Search by name or email"
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          className="search-input"
        />
      </div>

      {filtered.length > 0 ? (
        <div className="card-grid">
          {filtered.map((cust) => (
            <div key={cust.id} className="customer-card">
              <h3>{cust.first_name} {cust.last_name}</h3>
              <p className="email">{cust.email}</p>
              <p className="customer-id">ID: {cust.id}</p>
            </div>
          ))}
        </div>
      ) : (
        <p className="status-message">No matching customers found.</p>
      )}
    </div>
  );
};

export default CustomerList;
