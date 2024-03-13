# Vehicle-Access-Control-Gateway

一個基於 SOME/IP 協議的車輛訪問控制系統，使用 PEP（Policy Enforcement Point）、PDP（Policy Decision Point）和 Policy Engine 來管理對車輛功能的訪問。

## Architecture

該系統由以下組件組成：

1. `client.py`：模擬車輛的客戶端，發送訪問請求。
2. `pep.py`：Policy Enforcement Point，接收客戶端的訪問請求，並向 PDP 發出決策請求。
3. `pdp.py`：Policy Decision Point，接收來自 PEP 的決策請求，並向 Policy Engine 發出評估請求。
4. `policy_engine.py`：Policy Engine，評估訪問請求是否符合定義的策略，並返回決策結果。
5. `server.py`：SOME/IP 服務器，接收經過訪問控制的請求，並執行相應的操作。

## Steps

為了正確運行該系統，請按照以下順序啟動組件：

1. 首先，啟動 `policy_engine.py`：
   ```
   python3 policy_engine.py
   ```

2. 然後，啟動 `pdp.py`：
   ```
   python3 pdp.py
   ```

3. 接著，啟動 `pep.py`：
   ```
   python3 pep.py
   ```

4. 啟動 `server.py`：
   ```
   python3 server.py
   ```

5. 最後，運行 `client.py` 發送訪問請求：
   ```
   python3 client.py
   ```

## Procedure

1. `client.py` 生成一個 SOME/IP 訊息，其中包含要訪問的功能（如油門控制或剎車控制）及其參數。

2. `client.py` 將訪問請求發送到 `pep.py`。

3. `pep.py` 接收請求，並向 `pdp.py` 發出決策請求。

4. `pdp.py` 接收決策請求，並向 `policy_engine.py` 發出評估請求。

5. `policy_engine.py` 解析 SOME/IP 訊息，並根據定義的策略評估訪問請求。策略可以基於消息的內容（如特定的參數值）或其他因素。

6. `policy_engine.py` 返回決策結果（允許或拒絕）給 `pdp.py`。

7. `pdp.py` 將決策結果返回給 `pep.py`。

8. 如果訪問被允許，`pep.py` 將 SOME/IP 訊息轉發到 `server.py`；如果訪問被拒絕，`pep.py` 返回拒絕訊息給 `client.py`。

9. `server.py` 接收 SOME/IP 訊息，解析其內容，並執行相應的操作（如調整油門開度或剎車力度）。

## Configuration

- `pep.py`、`pdp.py` 和 `policy_engine.py` 使用 Flask 框架創建 HTTP 服務。它們之間通過 HTTP POST 請求進行通信。
- `pep.py` 運行在 `100.77.173.105:5000`，`pdp.py` 運行在 `100.77.173.105:5001`，`policy_engine.py` 運行在 `100.77.173.105:5002`。
- `pep.py` 實現了一個簡單的 HTTP 基本認證，用戶名和密碼存儲在程式碼中。在實際應用中，應使用更安全的認證方法。

## Policy Define

策略在 `policy_engine.py` 中定義。目前，系統中定義了以下策略函數：

- `malicious_signal_policy`：檢查煞車訊號中的特定值是否為 100。如果是，則拒絕訪問。
- `traffic_info_policy`：總是允許訪問。
- `vehicle_control_policy`：總是允許訪問。
- `risk_policy`：總是允許訪問。

---------------------------------------

# Vehicle-Access-Control-Gateway

A vehicle access control system based on the SOME/IP protocol that uses PEP (Policy Enforcement Point), PDP (Policy Decision Point), and Policy Engine to manage access to vehicle functions.

## Architecture

The system consists of the following components:

1. `client.py`: Simulates the vehicle client and sends access requests.

2. `pep.py`: Policy Enforcement Point, receives access requests from the client, and sends decision requests to the PDP.

3. `pdp.py`: Policy Decision Point, receives decision requests from the PEP, and sends evaluation requests to the Policy Engine.

4. `policy_engine.py`: Policy Engine, evaluates access requests against defined policies and returns decision results.

5. `server.py`: SOME/IP server, receives access-controlled requests and executes corresponding actions.

## Steps

To run the system correctly, start the components in the following order:

1. First, start `policy_engine.py`:

```
python3 policy_engine.py
```

2. Then, start `pdp.py`:

```
python3 pdp.py
```

3. Next, start `pep.py`:

```
python3 pep.py
```

4. Start `server.py`:

```
python3 server.py
```

5. Finally, run `client.py` to send access requests:

```
python3 client.py
```

## Procedure

1. `client.py` generates a SOME/IP message containing the function to be accessed (e.g., throttle control or brake control) and its parameters.

2. `client.py` sends the access request to `pep.py`.

3. `pep.py` receives the request and sends a decision request to `pdp.py`.

4. `pdp.py` receives the decision request and sends an evaluation request to `policy_engine.py`.

5. `policy_engine.py` parses the SOME/IP message and evaluates the access request against defined policies. Policies can be based on the message content (e.g., specific parameter values) or other factors.

6. `policy_engine.py` returns the decision result (allow or deny) to `pdp.py`.

7. `pdp.py` returns the decision result to `pep.py`.

8. If access is allowed, `pep.py` forwards the SOME/IP message to `server.py`; if access is denied, `pep.py` returns a denial message to `client.py`.

9. `server.py` receives the SOME/IP message, parses its content, and executes corresponding actions (e.g., adjusting throttle opening or brake force).

## Configuration

- `pep.py`, `pdp.py`, and `policy_engine.py` use the Flask framework to create HTTP services. They communicate with each other via HTTP POST requests.

- `pep.py` runs on `100.77.173.105:5000`, `pdp.py` runs on `100.77.173.105:5001`, and `policy_engine.py` runs on `100.77.173.105:5002`.

- `pep.py` implements a simple HTTP basic authentication, with the username and password stored in the code. In actual applications, more secure authentication methods should be used.

## Policy Define

Policies are defined in `policy_engine.py`. Currently, the following policy functions are defined in the system:

- `malicious_signal_policy`: Checks if a specific value in the brake signal is 100. If so, access is denied.

- `traffic_info_policy`: Always allows access.

- `vehicle_control_policy`: Always allows access.

- `risk_policy`: Always allows access.
