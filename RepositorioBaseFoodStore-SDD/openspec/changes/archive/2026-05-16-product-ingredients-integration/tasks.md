# TASKS: Product Ingredients Integration and Advanced Search-Select UI (Change #28)

## Phase 1: Database and Schema Modeling
- [x] 1.1. Declare intermediate Many-to-Many junction model `ProductIngrediente` mapping product and ingredient identifiers.
- [x] 1.2. Extend Pydantic schemas `ProductCreate` and `ProductUpdate` to support optional `ingredient_ids` list payloads.
- [x] 1.3. Define `ProductWithIngredients` schema returning flat `ingredientes` arrays to avoid deserialization loops.

## Phase 2: Test Infrastructure (TDD)
- [x] 2.1. Configure TestClient base prefix route in `backend/tests/products/test_products_router.py` to target `/api/v1`.
- [x] 2.2. Adapt existing integration assertions to scan relational returns under the Spanish label `ingredientes`.
- [x] 2.3. Run all test suites validating product relational mapping behavior.

## Phase 3: Core Backend Service Implementation
- [x] 3.1. Integrate atomic creation mapping in `ProductService.create_product`.
- [x] 3.2. Implement clean-up and mapping replacement logic in `ProductService.update_product`.
- [x] 3.3. Verify transactional changes roll back correctly in case of failure.

## Phase 4: Frontend API and Component Integration
- [x] 4.1. Update interface definitions in `frontend/src/shared/api/productsApi.ts` to include optional `ingredient_ids` parameters.
- [x] 4.2. Consume global ingredients list via React Query query state inside `ProductsAdminPage.tsx`.
- [x] 4.3. Implement custom async detail loader `handleOpenEdit` to fetch complete relationship structures prior to opening the edit modal.

## Phase 5: Search and Selection UI Polish
- [x] 5.1. Replace legacy checkboxes with query input field and compute reactive suggestion results (`useMemo`).
- [x] 5.2. Design absolute overlaid popover components displaying matching suggestions along with allergen indicator highlights.
- [x] 5.3. Bind inputs to a React `useRef` to trigger programmatical focus operations and clean state queries.
- [x] 5.4. Encapsulate selections as badges inside dynamic flex wrappers bounded by height and scroll-overflow styles.
