#encoding "utf8"

People -> Word<kwtype="places">;

Places -> Word<kwtype="people">;

Text -> AnyWord* People AnyWord*;

Text -> AnyWord* Places AnyWord*;

Text2 -> Text interp (Result.Name::not_norm);

