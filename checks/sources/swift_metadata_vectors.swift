// Owned static descriptor oracle; compiled to a dylib, never loaded or run.
public struct QuayValue {
    public var number: Int
    public var label: String
}
public enum QuayChoice {
    case empty
    case value(QuayValue)
}
public class QuayReference {
    public var count: Int = 0
    public var value: QuayValue? = nil
    public init() {}
}
