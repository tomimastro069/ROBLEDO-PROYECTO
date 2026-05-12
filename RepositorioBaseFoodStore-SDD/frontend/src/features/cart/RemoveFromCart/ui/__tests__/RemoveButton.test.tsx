import React from "react";
import { render, fireEvent } from "@testing-library/react";
import { RemoveButton } from "../RemoveButton";
import { useCartStore } from "@/entities/cart/model/cartStore";

jest.mock("@/entities/cart/model/cartStore");

describe("RemoveButton", () => {
  it("calls removeItem with itemId", () => {
    const removeItem = jest.fn();
    (useCartStore as jest.Mock).mockReturnValue(removeItem);
    const { getByRole } = render(<RemoveButton itemId={99} />);
    fireEvent.click(getByRole("button"));
    expect(removeItem).toHaveBeenCalledWith(99);
  });
});
