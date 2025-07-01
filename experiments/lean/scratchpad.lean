--- Random ---

#check fun(x : Nat) => x + 5

#check Nat.add
#check Nat.add 5

def α : Type := Nat
#check α

#eval (λ x y : Nat => x + y ) 10 12

def cons (α : Type) (a : α) (as : List α) : List α :=
  List.cons a as

#check cons


--- Proofs ---

--
set_option linter.unusedVariables false
--

-- difference between (p q : Prop) and {p q : Prop} ?
variable (p q : Prop)
--variable {p q : Prop}
theorem t1 : p → q → p :=
  fun (hp : p) (hq : q) => hp

--theorem t1 (p q : Prop) (hp : p) (hq : q) : p := hp
variable{a b c d : Prop}
-- wont compile if variable {p q : Prop} instead of variable (p q : Prop)
#check t1 a b

-- what does this work?
variable (p q r s : Prop)
theorem t2 (h₁ : q → r) (h₂ : p → q): p → r :=
  fun h₃ : p =>
  show r from h₁ (h₂ h₃)

variable (p q r s : Prop)
theorem t3 (h₁ : q → r) (h₂ : p → q) (h₃ : p): p → r :=
  fun h₄ : p =>
  show r from h₁ (h₂ h₃)

variable (p q r : Prop)
example (hp : p) (hq : q) : p ∧ q := And.intro hp hq
#check fun (hq : q) (hp : p) => And.intro hp hq

variable (p q : Prop)
example (h : p ∧ q) : q ∧ p :=
  And.intro (And.right h) (And.left h)

variable (p q : Prop)
example (h : p ∧ q) : q ∧ p :=
  ⟨h.right, h.left⟩

----
variable (p q : Prop)

theorem and_swap : p ∧ q ↔ q ∧ p :=
  Iff.intro
    (fun h : p ∧ q =>
     show q ∧ p from And.intro (And.right h) (And.left h))
    (fun h : q ∧ p =>
     show p ∧ q from And.intro (And.right h) (And.left h))

theorem and_swap_2 : p ∧ q ↔ q ∧ p :=
  ⟨ fun h => ⟨h.right, h.left⟩, fun h => ⟨h.right, h.left⟩ ⟩

#check and_swap_2 p q

variable (p q : Prop)

example (h : p ∧ q) : q ∧ p :=
  have hp : p := h.left
  have hq : q := h.right
  show q ∧ p from And.intro hq hp


variable (p q : Prop)

example (h : p ∧ q) : q ∧ p :=
  have hp : p := h.left
  suffices hq : q from And.intro hq hp
  show q from And.right h
