# TECHNICAL DESIGN: Product Ingredients Integration (Change #28)

## Architecture Overview
The Product Ingredients integration will be implemented using a relational association table to map products and ingredients. In the backend, a Many-to-Many junction model will process transactional requests atomically in a single Unit of Work session. In the frontend, an advanced react-query based async search-and-select flow will be integrated into the product administration modal, employing autofocus references and responsive height-locked containers to prevent visual distortion.

## Component Design

### 1. Database Junction Model
- **Table Name**: `ProductIngrediente`
- **Fields**: `product_id: int` (foreign key to `product`), `ingrediente_id: int` (foreign key to `ingrediente`).
- **Uniqueness Constraint**: Composite primary key on `(product_id, ingrediente_id)` to prevent duplicate mapping links.

### 2. Transactional Service Layer
- **File**: `backend/products/service.py`
- **Method updates**:
  - `create_product()`: Reconciles relational lists by associating passed `ingredient_ids` to the created product within the active Unit of Work session.
  - `update_product()`: Clears existing associated `ProductIngrediente` entities and regenerates fresh maps atomically, preventing database synchronization lag.

### 3. API Contract and Schemas
- **Path**: `backend/products/router.py`
- **Pydantic Schemas**:
  - `ProductCreate`: Includes `ingredient_ids: Optional[List[int]] = None`.
  - `ProductUpdate`: Includes `ingredient_ids: Optional[List[int]] = None`.
  - `ProductWithIngredients` (Spanish `ingredientes` mapping): Returns a serializable flat array of connected ingredients, mitigating circular deserialization recursion.

### 4. Search and Select UI Flow
- **Buscador Reactivo**: An input field using a React state `ingredienteSearch` and a `useMemo` filter matching search terms and excluding already selected badges.
- **Autofocus Ref**: Reference `searchInputRef` targeting the input element. Click handlers trigger input state resetting (`setIngredienteSearch('')`) to instantly hide suggestions and refocus programmatically using a micro `setTimeout` focus command.
- **Scroll Limit & Badge Layout**: Removable badges wrapped in a dynamic flex row. Container styles use `max-h-24` and `overflow-y-auto` to lock height and encapsulate long catalogs within a suttle scrollbar.

## Technical Constraints
- **Atomicity**: Reconciling database records for product ingredients must be executed within a single Unit of Work session transaction.
- **Recursion Avoidance**: Endpoint responses must avoid circular serializing lists by flattening ingredient models under the product representation.
- **Height Stability**: The frontend administration modal must remain static in physical height; ingredients selections must not push description/action elements down.

## Cross-Cutting Concerns
- **Allergen Alerting**: The interface must detect ingredients flagged as allergens (`es_alergeno: true`) and dynamically display warning badges (⚠️) for food safety compliance.
- **Async Hydration**: Upon click events on edit triggers, the client must trigger an explicit query to fetch detailed product relations before opening the modal, preventing partial list rendering.
