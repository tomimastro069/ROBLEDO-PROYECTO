# PROPOSAL: Product Ingredients Integration and Advanced Search-Select UI (Change #28)

## Intent
Integrate support for linking and reconciling ingredients with products from the user interface and the backend, complying with the food store requirements for allergen visibility and high-performance search controls.

## Problem
The current implementation of the catalog and product admin views lacks:
1. **Relational Database Linkage**: The database and backend router endpoints do not receive, validate, or store product-ingredient relationships.
2. **Catalog Scaling Visual Distortion**: The frontend creation modal render was based on static checkbox lists. In environments with hundreds or thousands of ingredients, this amontonamiento results in massive visual lag and modal deformation.
3. **Hydration Integrity**: Editing product parameters from list entries causes loss of ingredient associations because the list-products endpoint does not return nested relationship trees.
4. **Allergen Warnings**: Visual markers for food allergens are absent, violating dietary compliance standards.

## Proposed Changes
1. **Database Relational Setup**:
   - Establish Many-to-Many junction database model `ProductIngrediente`.
   - Update backend `ProductService` to atomically reconcile and update ingredient maps during product write operations.
2. **Backend API Schemas Refactoring**:
   - Update `ProductCreate` and `ProductUpdate` schemas to support list payloads of `ingredient_ids`.
   - Add Spanish serializing support `ingredientes` to `ProductWithIngredients` schema without circular deserialization recursion.
3. **Advanced Search-Select UI Component**:
   - Replace checkboxes with an input field linked to `ingredienteSearch` query state and a reactively computed suggested list (`useMemo`) that automatically filters matches and excludes already selected options.
   - Use absolute overlays (`absolute z-[150]`) to stack suggestion dropdown elements without pushing description blocks.
   - Implement programmatic autofocus with a React `useRef` and a click handler that instantly resets search queries and refocuses input elements.
   - Display selected ingredients as premium badges with dynamic `×` removal links, wrapping them inside a scroll-locked container (`max-h-24 overflow-y-auto`).

## Success Criteria
- [ ] `POST /api/v1/products` creates a product and successfully maps its relation array to `ProductIngrediente` table.
- [ ] `PATCH /api/v1/products/{id}` atomically updates the product, removing old relationships and establishing new ones cleanly.
- [ ] Allergen ingredients like 'Mussarela' display warning icons (⚠️) dynamically in suggestions and badge sections.
- [ ] Clicking a suggestion adds the ingredient, completely clears all suggestion lists, and immediately refocuses the input field programmatically.
- [ ] Modal visual dimensions remain strictly unchanged; scrolling is confined internally.
