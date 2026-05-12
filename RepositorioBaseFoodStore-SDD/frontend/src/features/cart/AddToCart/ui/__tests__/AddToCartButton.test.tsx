import React from "react";
import { render, fireEvent } from "@testing-library/react";
import { AddToCartButton } from "../AddToCartButton";
import { useCartStore } from "@/entities/cart/model/cartStore";

jest.mock("@/entities/cart/model/cartStore");

describe("AddToCartButton", () => {
  it("calls addItem with correct product and quantity", () => {
    const addItem = jest.fn();
    (useCartStore as jest.Mock).mockReturnValue(addItem);
    const product = { id: 42, name: "Hamburguesa", price: 1000, imageUrl: "test.jpg" };
    const { getByText } = render(
      <AddToCartButton product={product} initialQuantity={2} />
    );
    fireEvent.click(getByText(/Agregar al carrito/i));
    expect(addItem).toHaveBeenCalledWith({ ...product, quantity: 2 });
  });
});
