Prefer simple Model-View structure in SwiftUI.

- Views own lightweight UI orchestration.
- Services and models own business logic.
- Introduce a view model only when the codebase already leans on it or the feature truly needs that boundary.
- Splitting a large screen into smaller view types is usually a better first move than inventing a new view model.
