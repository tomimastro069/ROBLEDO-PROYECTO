import React from "react";
import { render, fireEvent } from "@testing-library/react";
import { QuantityControls } from "../QuantityControls";
import { useCartStore } from "@/entities/cart/model/cartStore";

jest.mock("@/entities/cart/model/cartStore");

describe("QuantityControls", () => {
  it("decrements quantity and disables at min", () => {
    const updateQuantity = jest.fn();
    (useCartStore as jest.Mock).mockReturnValue(updateQuantity);
    const { getByLabelText } = render(<QuantityControls itemId={1} quantity={2} min={1} />);
    fireEvent.click(getByLabelText(/Disminuir/i));
    expect(updateQuantity).toHaveBeenCalledWith(1, 1);
  });
  it("increments quantity and disables at max", () => {
    const updateQuantity = jest.fn();
    (useCartStore as jest.Mock).mockReturnValue(updateQuantity);
    const { getByLabelText } = render(<QuantityControls itemId={1} quantity={98} max={99} />);
    fireEvent.click(getByLabelText(/Aumentar/i));
    expect(updateQuantity).toHaveBeenCalledWith(1, 99);
  });
});
