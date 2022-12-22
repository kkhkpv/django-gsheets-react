import axios from "axios";
import { useEffect, useState } from "react";

const App = () => {
  const [orders, setOrders] = useState([]);

  const getOrders = async () => {
    try {
      const response = await axios.get(
        "http://localhost:8000/api/v1/orderlist/"
      );
      const data = await response.data;
      console.log(response);
      setOrders(data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    getOrders();
  }, []);

  return (
    <div className="grid">
      <table className="m-5">
        <thead className="text-center text-xs">
          <tr>
            <th>Order Number</th>
            <th>Cost</th>
            <th>Delivery Date</th>
            <th>Rouble cost</th>
          </tr>
        </thead>
        <tbody>
          {orders.map((order) => (
            <tr key={order.order_number} className="text-center text-xs">
              <td>{order.order_number}</td>
              <td>{order.cost}</td>
              <td>{order.delivery_date}</td>
              <td>{order.rouble_cost}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default App;
